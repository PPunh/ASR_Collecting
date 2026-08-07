# Context Processors
def theme_settings(request):
	# Set default theme when logout or none profile
	theme = 'w3-theme-blue.css'

	if request.user.is_authenticated:
		try:
			# Get profile of logined user
			theme = request.user.profile.theme_color
		except:
			pass

	return {
		'theme_color':theme
	}