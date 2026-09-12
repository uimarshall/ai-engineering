## The question

> The key principles are the:

1. The `Acceptance Criteria` (AC)
2. The `Critical Value` (CV)
3. The `T-Statistics`

> Assuming we choose an `AC` of `0.05` which is equivalent to `5%`, This implies that we have `5%` lies to the left of the `Normal Distribution` and `95%` lies to the Right.
> If the `t-statistics` is less than the AC or lies to the left, we say it is just `5%` chance that our hypothesis is likely correct, so we reject the `NH` and accepts the `AH`, otherwise if it is greater than the `AC`,i.e lies to the right, we say we have `95%` chance of being true, we accept the `NH`.

> ![alt text](image.png)

> Our `Alternate Hypothesis` is what we're testing for or what we're interested in.

> Acceptance criteria = 0.05

> The `AC` will act as a line in the sand around which we make our conclusions of which hypothesis (Null or Alternate) we think is more likely.
> ![alt text](image-1.png)

![alt text](image-2.png)

> Stats to use
>
> ![alt text](image-3.png)

> Formula - Welch's T-Test
>
> ![alt text](image-5.png)

> The `t-statistics` tells us where on the T-Distribution the difference in the two means lies and more specifically it helps us figure out how likely we are to see this difference in the `Means` if our `NH` (Null Hypo.) that the means are not different was true and from there based on our `AC` (Acceptance Criteria) we can come to some form of conclusions around whether we think there actually is a difference or if the difference we're seeing is down to noise or down to random chance.
>
> We're interested in whether our teams mean vertical leap is lower than that of rival team. We are running a `1-tailed-test` and thus we are concerned with the with the split on the left hand side of the distribution and the split point in dotted white line is known as the `critical value` where it splits the area under the distribution curve by our AC.
> If we get a `t-statistics` that is less than the `CV` (critical value), we are going to reject the NP. We are going to reject the idea that there is no difference between the means of our team ans our rival team in terms of the `vertical leap`.
> ![alt text](image-7.png)
> The vertical line Is known as the Critical Value where it splits the area under the distribution curve by our Acceptance Criteria, since we're using a value of 0.05, this splits the area with 5% on one side and 95% on the other side.

![alt text](image-6.png)

> If NP = True
>
> ![alt text](image-8.png)

> If it's less likely than our `AC`, then maybe it's not actually the case now conversely if we're using the formula and we obtain a `t-statistics` that was above the CV, we would fail to reject the NH. A `t-statistics` such as the the NH that there is no difference between the means is actually quite plausible or quite likely to be true.
>
> What the graph tells us if NH=True
>
> Essentially, er're saying if the NH is true we would expect to see `t-statistics` such as the one in the graph, one that falls within this range of values at least 95% of the time and because of that fact we might say it seems quite likely that the NH is actually true and because of that we would see no reason to reject that notion. Otherwise, we reject it and conclude that the differences between the two means was just down to noise or down to random chance.

![alt text](image-10.png)

![alt text](image-11.png)

> Find the degree of freedom
>
> ![alt text](image-13.png)

> Find the Critical value
> Find the intersection between the AC and DF to get the CV.
> ![alt text](image-14.png)

> Find the T-Statistic

![alt text](image-16.png)

![alt text](image-17.png)

The `t-statistic` value lands us in the 5% area under the distribution.

![alt text](image-18.png)

![alt text](image-19.png)

Conclusions

Formally, based on all of this, we reject the NH. And we would say something along the lines of an AC or significance level of 0.05 we reject the NH in favour of the AH. Which essentially translate to our team's, we have some confidence in the notion that our team's mean vertical leap is indeed significantly lower than that of our rival team!
![alt text](image-20.png)

![alt text](image-21.png)

![alt text](image-22.png)
