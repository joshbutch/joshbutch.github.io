<HEAD>  
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-116290644-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-116290644-1');
</script>
</HEAD>

<script type="text/javascript" src="https://platform.linkedin.com/badges/js/profile.js" async defer></script>

__My School__: I'm currently a graduate student in Denver, CO at Regis University. The program is a master's of science in data science, and I would highly recommend this program to anyone considering a graduate degree in this field. The entire program - curriculum, professors, support staff - have all exceeded my expectations. 

__About Me__: I have a young family so we are always on the go. We enjoy spending time in our garden and the great local parks in our neighborhood. We also like getting out to the foothills and mountains to do all of the outdoor things.

<div class="LI-profile-badge"  data-version="v1" data-size="medium" data-locale="en_US" data-type="horizontal" data-theme="dark" data-vanity="joshbutch"><a class="LI-simple-link" href='https://www.linkedin.com/in/joshbutch?trk=profile-badge'>Josh Butch</a></div>

***
__Technology Interests__: <br><br>Artificial Neural Networks, Deep Learning, Computer Vision, Streaming Video Analysis<br>
                          Python - pandas, matplotlib, OpenCV, plotly, Bokeh - Jupyter Notebooks<br>
                          R - ggplot2, caret, randomForest, plyr, stringr - RStudio<br>
                          Tableau<br>
                          RapidMiner<br>
                           
***
__Intention of My Blog__: To track the progress of, and have dialogue about, my final practicum project due Aug. 2019.

***
### Meet JANN (Josh's Artificial Neural Network)

JANN will hopefully be the final practicum project for my graduate degree.  My goal is to build a deep learning neural network that will analyze real-time video for object detection and subsequent action.  I feel there are applications for this technology in every industry.  Computer vision is obviously a focus of the industry and also something I find very interesting, so I feel this project will blend many of my data science aspirations.  In the end, I hope to show enough proficiency and promise to warrant continued work post graduation.

There will be a few iterations of JANN as the final positive image training set will need to be mined over the next few months.  I'm narrowing down JANN's final scope, but it's difficult for many reasons.  I haven't completely landed on the specific end task to be accomplished by JANN, as I imagine my faculty advisor will have input/requirements.  I do have some ideas about how to begin the project.

My first goal is to build a basic neural network with OpenCV that will be trained to detect and count the loose change thrown into the video frame.  I chose this idea because it is relevant to multiple industries (gaming, transportation, etc.), it will only require a small positive training set, and I believe I will be able to easily mine a negative image training set because loose change is not prevalent in most pictures.  Once I manage to get that to work, I will hopefully have worked through enough of the code to be able to apply it to subsequent training sets to broaden JANN's "vision." Perhaps even open it up to additional currencies with an instant currency converter.  The newest version of OpenCV comes with a dnn package: deep neural networks.  From what I've read so far this will be my starting point as soon as the project is approved.

```python
print("Hello World, I'm JANN!")
```





