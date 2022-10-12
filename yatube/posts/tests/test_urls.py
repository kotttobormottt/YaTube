from http import HTTPStatus

from django.core.cache import cache
from django.test import Client, TestCase

from ..models import Group, Post, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.user_non = User.objects.create_user(username="noauth")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test_slug",
            description='Тестовое описание группы'
        )
        cls.post = Post.objects.create(
            text="Тестовый текст",
            author=cls.user
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_no_posts = Client()
        self.authorized_client_no_posts.force_login(self.user_non)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            "/": "posts/index.html",
            f"/group/{PostURLTests.group.slug}/": "posts/group_list.html",
            f"/profile/{self.user}/": "posts/profile.html",
            f"/posts/{int(self.post.pk)}/": "posts/post_detail.html",
            f"/posts/{int(self.post.pk)}/edit/": "posts/create_post.html",
            "/create/": "posts/create_post.html",
            '/follow/': 'posts/follow.html',
            '/unexisting_page/': 'core/404.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_404(self):
        """Если страница не найдена на сайте, возвращает код ответа 404"""
        response = self.authorized_client.get("/404/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_uses_correct_access_guest(self):
        """URL-адрес доступен или нет не авторизированному пользователю."""
        code_answer_for_users = {
            "/": HTTPStatus.OK,
            f"/group/{PostURLTests.group.slug}/": HTTPStatus.OK,
            f"/profile/{self.user}/": HTTPStatus.OK,
            f"/posts/{int(self.post.pk)}/": HTTPStatus.OK,
            f"/posts/{int(self.post.pk)}/edit/": HTTPStatus.FOUND,
            "/create/": HTTPStatus.FOUND,
            "/unexisting_page/": HTTPStatus.NOT_FOUND,
        }
        for address, code in code_answer_for_users.items():
            with self.subTest(address=address):
                cache.clear()
                response = self.client.get(address)
                self.assertEqual(response.status_code, code)

    def test_urls_uses_correct_access_auth(self):
        """URL-адрес доступен авторизированному пользователю."""
        code_answer_for_users = {
            "/": HTTPStatus.OK,
            f"/group/{PostURLTests.group.slug}/": HTTPStatus.OK,
            f"/profile/{self.user}/": HTTPStatus.OK,
            f"/posts/{int(self.post.pk)}/": HTTPStatus.OK,
            f"/posts/{int(self.post.pk)}/edit/": HTTPStatus.OK,
            "/create/": HTTPStatus.OK,
            "/unexisting_page/": HTTPStatus.NOT_FOUND,
        }
        for address, code in code_answer_for_users.items():
            with self.subTest(address=address):
                cache.clear()
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, code)

    def test_urls_uses_correct_access_auth_edit(self):
        """URL-адрес редактирования не доступен пользователю."""
        code_answer_for_users = {
            "/": HTTPStatus.OK,
            f"/group/{PostURLTests.group.slug}/": HTTPStatus.OK,
            f"/profile/{self.user}/": HTTPStatus.OK,
            f"/posts/{int(self.post.pk)}/": HTTPStatus.OK,
            f"/posts/{int(self.post.pk)}/edit/": HTTPStatus.FOUND,
            "/create/": HTTPStatus.OK,
            "/unexisting_page/": HTTPStatus.NOT_FOUND,
        }
        for address, code in code_answer_for_users.items():
            with self.subTest(address=address):
                cache.clear()
                response = self.authorized_client_no_posts.get(address)
                self.assertEqual(response.status_code, code)
