_Revolution Slider is not currently used by the CSHC website._

I've removed it from source control as it contains ~1700 files that all get copied to S3 every time `manage.py collectstatic` is called (slow and costly).

If you want to make use of the Revolution Slider, just re-add the source code (found in the Unify theme release) to this directory.
