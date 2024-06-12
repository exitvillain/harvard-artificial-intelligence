So i started by using the model Brian had in lecture and i started by only adjusting the parameters that
were absolutely necesary such as adjusting the input shape to 30 by 30 and change the color from black and white
to color by changing the final argument by 1 to 3.  I ran this network and got under 90 percent accuracy. My next
plan was to change the dropout while keeping the one hidden layer. When i tried a dropout of .5, i got a terrible accuracy
of .0547.  So then i changed it to .01 and i got a much better accuracy of .9275 and sometimes i even got .94. 
So there i noticed that the same exact parameters might give you different results.  This is because adjusting the weights
on these neural networks isn't an exact science. Different things can happen each time. So noticing that decreasing the dropout 
actually helped my final accuracy, i decided to try it with  no dropout. I got an accuracy of .9148. Ok, so that means
that .1 was some kind of sweet spot so i decided to settle on that. I didn't have much success adding other hidden layers.
I tried adding a hidden layer with 512 nodes, than 256 all with pretty terrible results.  I also tried using a tanh 
activiation function as the first activation function used in the .conv2D object. I was thinking using tanh might
help normalize my results since a tan function can never take input values between -1 and 1. if you google tanh function, 
you will see that there are vertical assymtotes at 1 and -1. Anyway, this didn't have much affect. I was getting similar 
accuracies. so i decided to go back to relu with just one hidden layer and a dropout of .1 coming after that. I was able to 
reach .95 accuracy on this. 
