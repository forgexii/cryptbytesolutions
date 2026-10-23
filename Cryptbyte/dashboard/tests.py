"""
Cryptbyte Solutions - Automated Regression & Security Test Suite

Tests core utilities, authentication authorization, open redirect defenses,
public view availability, portfolio relationships, and form validation security.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from Cryptbyte.utils import (
    generate_unique_slug,
    generate_initials,
    split_comma_string,
    parse_json_list,
)
from teams.models import Department, Specialization, TeamMember
from blogs.models import BlogPost, BlogCategory
from solutions.models import Solution
from projects.models import Project


class CentralUtilsTestCase(TestCase):
    """Verifies core utility functions in Cryptbyte/utils.py."""
    def test_generate_initials(self):
        self.assertEqual(generate_initials('Marcus Vance'), 'MV')
        self.assertEqual(generate_initials('Vance'), 'VA')
        self.assertEqual(generate_initials(''), 'CB')
        self.assertEqual(generate_initials(None), 'CB')

    def test_split_comma_string(self):
        self.assertEqual(split_comma_string('Python, Django , Celery'), ['Python', 'Django', 'Celery'])
        self.assertEqual(split_comma_string(''), [])
        self.assertEqual(split_comma_string(None), [])

    def test_parse_json_list(self):
        self.assertEqual(parse_json_list('[{"key": "val"}]'), [{'key': 'val'}])
        self.assertEqual(parse_json_list('invalid-json'), [])
        self.assertEqual(parse_json_list(''), [])
        self.assertEqual(parse_json_list(None), [])

    def test_generate_unique_slug(self):
        post1 = BlogPost.objects.create(title='AI Revolution')
        post2 = BlogPost.objects.create(title='AI Revolution')
        self.assertEqual(post1.slug, 'ai-revolution')
        self.assertEqual(post2.slug, 'ai-revolution-1')


class DashboardSecurityTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staff_test',
            password='Password123!',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regular_test',
            password='Password123!',
            is_staff=False
        )

    def test_unauthenticated_redirect(self):
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('dashboard:login'), response.url)

    def test_non_staff_redirect(self):
        self.client.login(username='regular_test', password='Password123!')
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('dashboard:login'), response.url)

    def test_staff_access(self):
        self.client.login(username='staff_test', password='Password123!')
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)

    def test_open_redirect_prevented(self):
        # Ensure external redirect URLs are blocked and redirected to dashboard:home
        malicious_urls = [
            'https://evil-attacker-site.com',
            '//evil-attacker-site.com/exploit',
            'javascript:alert(1)',
        ]
        for bad_url in malicious_urls:
            with self.subTest(bad_url=bad_url):
                response = self.client.post(
                    f"{reverse('dashboard:login')}?next={bad_url}",
                    {'username': 'staff_test', 'password': 'Password123!'}
                )
                self.assertRedirects(response, reverse('dashboard:home'))

    def test_safe_relative_next_allowed(self):
        # Ensure safe relative internal redirect URLs are honored
        safe_url = reverse('dashboard:blog_list')
        response = self.client.post(
            f"{reverse('dashboard:login')}?next={safe_url}",
            {'username': 'staff_test', 'password': 'Password123!'}
        )
        self.assertRedirects(response, safe_url)


class PublicEndpointsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_public_pages_load(self):
        routes = [
            'home:home',
            'about:about',
            'services:services',
            'solutions:solutions',
            'projects:projects',
            'teams:teams',
            'blogs:blogs',
            'contact:contact',
        ]
        for route in routes:
            with self.subTest(route=route):
                response = self.client.get(reverse(route))
                self.assertEqual(response.status_code, 200)


class TeamMemberPortfolioTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.member = TeamMember.objects.create(
            name='Ada Lovelace',
            role='Lead Systems Architect',
            portfolio_url='https://adalovelace.dev'
        )

    def test_portfolio_model_property(self):
        self.assertEqual(self.member.portfolio, 'https://adalovelace.dev')

    def test_team_detail_name_links_to_portfolio(self):
        response = self.client.get(reverse('teams:team_detail', kwargs={'pk': self.member.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="https://adalovelace.dev"')
        self.assertContains(response, 'member-portfolio-link')
        self.assertContains(response, 'Ada Lovelace')

    def test_team_detail_without_portfolio(self):
        member_no_url = TeamMember.objects.create(
            name='Charles Babbage',
            role='Computer Pioneer'
        )
        response = self.client.get(reverse('teams:team_detail', kwargs={'pk': member_no_url.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'member-portfolio-link')
        self.assertContains(response, 'Charles Babbage')


class FormValidationSecurityTestCase(TestCase):
    def test_solution_form_invalid_json_rejected(self):
        from dashboard.forms import SolutionForm
        form = SolutionForm(data={
            'title': 'Test Solution',
            'slug': 'test-solution',
            'category': 'Enterprise',
            'metrics_json': '{not-valid-json}',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('metrics_json', form.errors)

    def test_solution_form_valid_json_accepted(self):
        from dashboard.forms import SolutionForm
        form = SolutionForm(data={
            'title': 'Valid Solution',
            'slug': 'valid-solution',
            'category': 'Enterprise',
            'metrics_json': '[{"value": "99.9%", "label": "Uptime", "desc": "High availability"}]',
        })
        self.assertTrue(form.is_valid(), form.errors)
