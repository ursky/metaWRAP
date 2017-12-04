#!/usr/bin/env python
# USAGE:
# ./script file1.stats file2.stats file3.stats

import sys
import matplotlib.pyplot as plt
plt.switch_backend('agg')

max_contamination=10
min_completion=50

####################################################################################################################################
############################################         MAKE THE COMPLETION PLOT           ############################################
####################################################################################################################################
print "Loading completion info...."
data={}
max_x=0
# loop over all bin .stats files
for file_name in sys.argv[1:]:
	bin_set=".".join(file_name.split("/")[-1].split(".")[:-1])
	data[bin_set]=[]
	for line in open(file_name):
		# skip header
		if "compl" in line: continue

		# skip bins that are too contaminated or very incomplete
		if float(line.split("\t")[2])>max_contamination: continue
		if float(line.split("\t")[1])<1: continue

		# save the completion value of each bin into a list
		data[bin_set].append(float(line.split("\t")[1]))
	if len(data[bin_set])>max_x: max_x=len(data[bin_set])

# sort the completion data sets
for bin_set in data:
	data[bin_set].sort(reverse=True)

print "Plotting completion data..."
# MAKING THE PLOT PRETTY!!!!
# set some color schemes
tableau20 = [(214, 39, 40), (31, 119, 180), (255, 127, 14),    
             (44, 160, 44), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

for i in range(len(tableau20)):    
	r, g, b = tableau20[i]    
	tableau20[i] = (r / 255., g / 255., b / 255.)
plot_colors={}
for i, label in enumerate(sys.argv[1:]):
	bin_set=".".join(label.split("/")[-1].split(".")[:-1])
	plot_colors[bin_set]=tableau20[i]



# set figure size
plt.figure(figsize=(16, 8))
plt.style.use('ggplot')

# Remove the plot frame lines. They are unnecessary chartjunk.    
ax = plt.subplot(121)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.5)
ax.spines['bottom'].set_color('black')
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.set_facecolor('white')

# Ensure that the axis ticks only show up on the bottom and left of the plot.    
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# Limit the range of the plot to only where the data is.    
plt.ylim(-5, 105)
max_x=0
for k in data:
	if len(data[k])>max_x: max_x=len(data[k])
plt.xlim(0, max_x)

# Make sure your axis ticks are large enough to be easily read.    
plt.yticks(range(0, 105, 10), [str(x) + "%" for x in range(0, 105, 10)], fontsize=14)    
plt.xticks(fontsize=14)    

# Provide tick lines across the plot to help your viewers trace along    
for y in range(0, 105, 10):    
	plt.plot(range(0, max_x), [y] * len(range(0, max_x)), "--", lw=0.5, color="black", alpha=0.3)    
  
# Remove the tick marks; they are unnecessary with the tick lines we just plotted.    
plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")    


# PLOTTING THE DATA

# prepare labeles
labels = []
for k in data: labels.append(k)

# start plotting data
for rank, bin_set in enumerate(labels):
	# chose a color!
	c=plot_colors[bin_set]

	# plot the data
	plt.plot(data[bin_set], lw=2.5, color=c)
	
	# add bin set label to plot
	y_pos = data[bin_set][len(data[bin_set])*3/4]
	x_pos=len(data[bin_set])*3/4
	plt.text(x_pos, y_pos, bin_set, fontsize=14, color=c)

# add plot and axis titles and adjust edges
plt.title("Bin completion ranking", fontsize=26) 
plt.xlabel("Descending completion rank", fontsize=16)
plt.ylabel("Estimated bin completion", fontsize=16)




####################################################################################################################################
############################################         MAKE THE CONTAMINATION PLOT        ############################################
####################################################################################################################################
print "Loading contamination info..."

data={}
# loop over all bin .stats files
for file_name in sys.argv[1:]:
	bin_set=".".join(file_name.split("/")[-1].split(".")[:-1])
	data[bin_set]=[]
	for line in open(file_name):
		# skip header
		if "compl" in line: continue

		# skip bins that are too incomplete or way too contaminated
		if float(line.split("\t")[1])<min_completion: continue
		if float(line.split("\t")[2])>1000: continue

		# save the contamination value of each bin into a list
		data[bin_set].append(float(line.split("\t")[2]))

# sort the contamination data sets
for bin_set in data:
	data[bin_set].sort(reverse=False)

print "Plotting the contamination data..."
# MAKING THE PLOT PRETTY!!!!
# Remove the plot frame lines. They are unnecessary chartjunk.    
ax = plt.subplot(122)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.5)
ax.spines['bottom'].set_color('black')
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.set_facecolor('white')

# Ensure that the axis ticks only show up on the bottom and left of the plot.    
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# Limit the range of the plot to only where the data is.    
#plt.gca().invert_yaxis()
plt.ylim(0.06, 1600)
ax.set_yscale('log')
max_x=0
for k in data:
	if len(data[k])>max_x: max_x=len(data[k])
plt.xlim(0, max_x)

# Make sure your axis ticks are large enough to be easily read.    
plt.yticks([0.1,1,10,100,1000], ["0.1%","1%","10%","100%","1000%"], fontsize=14)
plt.xticks(fontsize=14)    

# Provide tick lines across the plot to help your viewers trace along    
for y in [0.1,1,10,100,1000]:    
	plt.plot(range(0, max_x), [y] * len(range(0, max_x)), "--", lw=0.5, color="black", alpha=0.3)    
  
# Remove the tick marks; they are unnecessary with the tick lines we just plotted.    
plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")    


# PLOTTING THE DATA
# prepare labeles
labels = []
for k in data: labels.append(k)


# start plotting data
for rank, bin_set in enumerate(labels):
	# chose a color!
	c=plot_colors[bin_set]

	# plot the data
	plt.plot(data[bin_set], lw=2.5, color=c)
	
	# add plot label
	x_pos = len(data[bin_set])-1
	y_pos = data[bin_set][-1]
	plt.text(x_pos, y_pos, bin_set, fontsize=14, color=c)

# add plot and axis titles and adjust the edges
plt.title("Bin contamination ranking", fontsize=26) 
plt.xlabel("Acending contamination rank", fontsize=16)
plt.ylabel("Estimated bin contamination (log scale)", fontsize=16)
plt.gcf().subplots_adjust(right=0.9)

# save figure
print "Saving figures binning_results.eps and binning_results.png ..."
plt.tight_layout(w_pad=10)
plt.subplots_adjust(top=0.92, right=0.90, left=0.08)
plt.savefig("binning_results.eps",format='eps', dpi=600)
plt.savefig("binning_results.png",format='png', dpi=600)
#plt.show()






