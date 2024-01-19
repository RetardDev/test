from django.db import models
from .userprofile import UserProfile
from .service import Services
from .provider import Provider

class Reviews(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    @staticmethod
    def get_reviews_by_service(service_id):
        return Review.objects.filter(service_id=service_id)

    @staticmethod
    def average_rating(self):
        sum = 0
        reviews = Reviews.object.filter(service=self.service)
        for rating in reviews:
            sum += reviews.rating
        average = sum / len(reviews)
        return average

    def __str__(self):
        return self.client.email