from django.contrib.auth.models import User
from image_loader.image.models import MainImage, Image
from image_loader.plan.models import UserPlan, Plan
from rest_framework.test import APITestCase
from django.urls import reverse
from django.core.files import File


class TestAPI(APITestCase):

	@classmethod
	def setUpTestData(cls):
		"""
		Mock some objects
		"""

		enterprise_user = User.objects.create_user(
			username="enterprise",
			password="enterprise",
		)
		enterprise_plan = Plan.objects.create(
			plan_name="Enterprise",
			allowed_sizes="200 400",
			acces_to_the_og=True,
			ability_to_generate_expiring_links=True,
		)
		UserPlan.objects.create(
			user=enterprise_user,
			plan=enterprise_plan
		)

		basic_user = User.objects.create_user(
			username="basic",
			password="basic",
		)
		basic_plan = Plan.objects.create(
			plan_name="Basic",
			allowed_sizes="200",
			acces_to_the_og=False,
			ability_to_generate_expiring_links=False,
		)
		UserPlan.objects.create(
			user=basic_user,
			plan=basic_plan
		)
		

	def test_get_allowed_sizes(self):
		"""
		test if obj method returns correct data
		"""
		plan = Plan.objects.get(plan_name="Enterprise")
		self.assertEqual(plan.get_allowed_sizes(), ["200", "400"])

		plan = Plan.objects.get(plan_name="Basic")
		self.assertEqual(plan.get_allowed_sizes(), ["200"])

	def test_image_main_view_set_basic(self):
		"""
		image uploader, Basic Plan
		"""
		url = reverse("image:mainimage-list")
		response = self.client.get(url)
		self.assertEqual(response.status_code, 403) ## because of unauth

		user = User.objects.get(username="basic")
		self.client.force_authenticate(user)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200) ## auth, OK

		data = {}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 400) ## beacuse of empty image
		data["image"] = File(open("media/test/test.jpg", "rb"))
		response = self.client.post(url, data)
		self.assertEqual(response.data["image_name"], "test")
		images = response.data["images"]
		self.assertEqual(len(images), 1) ## just image of size 200

		data = {}
		data["image"] = File(open("media/test/test.bmp", "rb"))
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 400) ## because of the incorrect extension
		self.assertEqual(str(response.data["image"][0]), "Incorrect file!")

		data["image"] = File(open("media/test/test.jpg", "rb"))
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 400) ## same file already exists

	def test_image_main_views_set_and_detail_enterprise(self):
		"""
		image uploader, Enerprise Plan

		"""
		user = User.objects.get(username="enterprise")
		self.client.force_authenticate(user)
		url = reverse("image:mainimage-list")
		data = {}
		data["image"] = File(open("media/test/test.jpg", "rb"))
		response = self.client.post(url, data)
		self.assertEqual(len(response.data["images"]), 3) ## 200, 400 and original photo
		
		url = reverse("image:mainimage-detail", kwargs={"image_name": "test"})
		response = self.client.get(url)
		self.assertEqual(response.data["image_name"], "test")
		self.assertEqual(len(response.data["images"]), 3) ## 200, 400 and original photo

	def test_generate_link_api_view(self):
		"""
		generating temporary links to images
		"""
		url = reverse("image:mainimage-list")
		data = {}
		data["image"] = File(open("media/test/test.jpg", "rb"))

		user = User.objects.get(username="enterprise")
		self.client.force_authenticate(user)
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 201)

		url = reverse("image:generate-link")
		data = {
			"expires_after": 1000,
			"size": 200,
			"image_name": "test"
		}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 200)
		link = response.data["link"]
		response = self.client.get(link)
		self.assertEqual(response.status_code, 200)