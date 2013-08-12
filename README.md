# Stripe Payment App

### How to Get Started

1. Install all the necessary packages (best done inside of a virtual environment)
> pip install -r requirements.txt

3. Run the app
> python runserver.py

4. Make sure 'mongod' is installed and running - http://docs.mongodb.org/manual/installation/

5. Add PUBLISHABLE_KEY and SECRET_KEY to your .basrc file
> export PUBLISHABLE_KEY=<your_publishable_key_from_stripe> 
> export SECRET_KEY=<your_secret_key_from_stripe>
and reload bashrc
> . ~/.bashrc

### Author(s) 

Muneeb Ali - http://muneeb.org
Modified from examples at http://stripe.com/docs/

### License

MIT License - see LICENSE 
