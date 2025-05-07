Para calcular la integral ∫₀¹ x² dx, podemos utilizar el método de integración por partes.

La fórmula de integración por partes es:

∫u dv = uv - ∫v du

donde u y v son funciones que satisfacen las condiciones:

u(0) = 0
u'(x) = v'(x)

En este caso, podemos elegir:

u(x) = x²
v(x) = x

Entonces, tenemos:

u(0) = 0² = 0 (condición 1)
u'(x) = 2x = v'(x) (condición 2)

Ahora, podemos aplicar la fórmula de integración por partes:

∫x² dx = uv - ∫v du
= x² * x - ∫x * 2x dx

Para calcular el último término, podemos nuevamente utilizar el método de integración por partes. Esta vez, elegimos:

u(x) = x
v(x) = x

Entonces, tenemos:

u(0) = 0
u'(x) = 1 = v'(x)

Ahora, podemos aplicar la fórmula de integración por partes nuevamente:

∫x dx = uv - ∫v du
= x * x - ∫x * 1 dx

Resolviendo el último término, obtenemos:

∫x dx = (x²)/2

Ahora, podemos reemplazar este resultado en la ecuación anterior:

∫x² dx = x² * x - (x²)/2
= x³ - (x²)/2 + C

donde C es el constante de integración.

Para encontrar el valor de C, podemos utilizar las condiciones de límite:

C = ∫x² dx|₀¹
= (1³) - ((0²))/2
= 1

Entonces, la integral original se puede escribir como:

∫x² dx = x³ - (x²)/2 + 1

Ahora, podemos evaluar esta integral en los límites del intervalo [0,1]:

∫₀¹ x² dx = [(1³) - ((1²))/2] - [(0³) - ((0²))/2]
= 1 - (1/2) - 0
= 1/2

