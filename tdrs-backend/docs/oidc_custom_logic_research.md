# Details in Regards to the Custome OIDC Logic

We are currently using a custom implementation of OIDC authentication due to the limitations of exiting django OIDC libraries. This decision was derivied out of necessity due to existing libraries such as [mozilla-django-oidc](https://github.com/mozilla/mozilla-django-oidc/blob/master/mozilla_django_oidc/auth.py#L222-L230) providing no option to append the client_assertion needed in the call to [Login.gov/token](https://developers.login.gov/oidc/#token). Other libraries provide less options as they are more geared towards using OpenID Connect protocols implemented by Google and Social Media Platforms. 


## Status

We are currently researching the use of the django library [drf-oidc-auth](https://github.com/ByteInternet/drf-oidc-auth) which we can leverage to replace some of the id_token verification logic we have created but still not a viable replacment for the Login.gov authentication process we have to implement. 

Also, we are looking into  forking one of the existing opensource Github repos and adjust their code base to suit our needs, however this brings us back to the added risk of writing our own custom code to handle this process. 

## Decision

Until an adequate alternative can be found, we will continue to use our custom code. 

## Consequences

There is an added risk of needing to support our own OIDC authentication logic due to the development team being directly responsible for its security and maintenance. 