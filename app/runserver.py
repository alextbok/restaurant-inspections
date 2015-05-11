from application import app
from application.db import setup
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--development", 
		help="Run in development mode with debugging enabled on port 5000.",
		action="store_true",
		default=False)
(options, args) = parser.parse_args()

if __name__=="__main__":
	if options.development:
		app.run(debug=True)
	else:
		aap.run(host='0.0.0.0', port=80)