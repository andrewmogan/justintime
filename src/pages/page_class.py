class page:
	def __init__(self, name, id):
		self.name = name
		self.id = id
		self.plots =[]
	
	def add_plot(self, plot):
		if isinstance(plot, list):
			self.plots.extend(plot)
		elif isinstance(plot, str):
			self.plots.append(plot)