+++
title = "Math example"
date = 2026-10-11
description = "Testing equations and plots on the new site."

[taxonomies]
tags = ["math"]

[extra]
math = true
+++

Here's some inline math: $y = x^2$. And some display math:

<div>
$$
\begin{equation}
\frac{1}{2} = \frac{2}{4}.
\end{equation}
$$
</div>

Below is a parabola.

{{ <figure src="plot.svg" alt="Graph of the parabola y = x squared for x from -2 to 2" caption="This is a caption with some math: $y = x^2$." width="503" height="322" page /> }}

Some more: $\\{1,2,3\\}$.
