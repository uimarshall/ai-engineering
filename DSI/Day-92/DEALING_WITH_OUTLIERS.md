An `outlier` can be any value that `differs significantly` from other values.

The perception of what an `outlier` is depends on the scenario you're dealing with. Given a particular scenario, you could just say that an `outlier` is any value that seems out of place in our data. But just because a number is very large or very small, it doesn't instantly mean it shouldn't be there. You could argue that every value, no matter how high or low, is genuinely part of the data, and therefore we shouldn't consider removing them at all.

But the problem with `outlier` is that they can cause issues for understanding things like averages as well as skewing the learning in certain machine learning models, making them perform worse across the vast majority of data points.

## How to deal with `outliers`

![alt text](image.png)

> The easiest approach is to do nothing at all, we'll just leave the data as it is.

> The second option is to remove any rows of data that contain `outlier` values in one or more of the columns. This is a pretty good option if you're in a scenario where `outliers` will have a big impact on how the model learns.

> Thirdly, we could keep the `outliers` in our data, but replace their values with something else. This can be a good solution in cases where you're low on data, as it allows you to keep all rows, but avoid the problems that the `outliers` cause. One downside of this particular approach is that we're essentially manipulating the real data. If you have enough data, It might be often better to remove the rows rather than apply this approach.

In terms of replacing values, there isn't one way of doing this, You could easily replace all `outliers` with the `mean` or `median` value, or you could apply an approach known as `Windsor Rising`, where we replace `outliers` with the closest value in our data that isn't deemed to be an outlier anyway.

## Why we should deal with `outliers`
