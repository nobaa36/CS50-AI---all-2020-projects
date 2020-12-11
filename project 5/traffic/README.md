Well I started with same settings as in video...

    model.add(tf.keras.layers.Conv2D(32,(3,3), activation="relu", input_shape=(30, 30, 3)))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(128, activation="relu"))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(NUM_CATEGORIES , activation="softmax"))

and received result of accuracy = 22%.

...well ok, I have a start point. 

I've reduced hidden layer to 64 and got 17 % 
I've increased hidden layer to 256 and got 37%.
Quickly realized that adding a lot of neurons to hidden layer leads to overfiting...
... so I add more hidden layers and found out that I have overfitted model again :)

Decided to started over.
I added one and more convolutional layers , experimenting with filters and kernels figured out that 
every next conv2d layer with higher amount of filters gives me better results.

Sadly , I couldn't get more then 50%. 
After a long research found out that numpy resizing works differently then cv2 resizing.

When I change line

    img.resize(IMG_WIDTH, IMG_HEIGHT, 3)
to

    img = cv2.resize(img , (IMG_WIDTH, IMG_HEIGHT))
    
I got 95% !!

Now, using previous experience, I adjusted layers and parameters and got 98%.
Reducing dropdown a bit to 0.4 ultimately gave me 99%


