_jquery-ui themes are not currently used by the CSHC website._

I've removed all but the base theme from source control to reduce the number of static files that get copied to S3 every time `manage.py collectstatic` is called (slow and costly).

If you want to make use of another jquery-ui theme, just re-add the relevant theme folder (found in the Unify theme release) to this folder.
