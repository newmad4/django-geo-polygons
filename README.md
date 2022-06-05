## SRS:
Prompt:

As Company_name expands internationally, we have a growing problem that many transportation suppliers we'd like to integrate cannot give us concrete zip codes, cities, etc that they serve.


To combat this, we'd like to be able to define custom polygons as their "service area" and we'd like for the owners of these shuttle companies to be able to define and alter their polygons whenever they want, eliminating the need for company employees to do this boring grunt work.


### Requirement:

- Build a JSON REST API with CRUD operations for Provider (name, email, phone number, language and currency) and ServiceArea (name, price, geojson information)
- Create a specific endpoint that takes a lat/lng pair as arguments and return a list of all polygons that include the given lat/lng. The name of the polygon, provider's name, and price should be returned for each polygon. This operation should be FAST.
- Use unit tests to test your API;
- Write up some API docs (using any tool you see fit);
- Create a Github account (if you don’t have one), push all your code and share the link with us;
- Deploy your code to a hosting service of your choice. Company_name is built entirely on AWS, so bonus points will be awarded for use of AWS.

### Considerations:
- All of this should be built in Python/DjangoRest.
- Use any extra libraries you think will help, choose whatever database you think is best fit for the task, and use caching as you see fit.
- Ensure that your code is clean, follows standard PEP8 style (though you can use 120 characters per line) and has comments where appropriate.
- It should take you 8-10 hours to complete and we give you 48 hours to send it back to us.
- We will not look at any attachments, screenshots or files sent by you, only Github and your deployed server.

### My assumptions and thoughts:
1) Coordinate system is "DD.DDDDD", so lat/lng is looks like: 50.6791688
2) For lat, lng args in polygons URL need another check as regexp make slower check this parameters.