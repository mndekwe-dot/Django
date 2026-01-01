from rest_framework.decorators import APIView
import logging
import requests

logger= logging.getLogger(__name__)    # configure logger
class HelloView(APIView):
    def get(self, request):
        try:    
            logger.info('calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('httpbin responded')
            data = response.json()
            return render(request, "Hello.html", {"name": data})
        except requests.ConnectionError as e:
            logger.critical('httpbin is down')
        return render(request, "Hello.html", {"name": "Error occurred"})    