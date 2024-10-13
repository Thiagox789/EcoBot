a=1
contador_plastico=0
contador_vidrio=0
contador_metal=0
if a == 1:
    contador_plastico = max(0, contador_plastico - 1)
elif a==2:
    contador_vidrio = max(0, contador_vidrio - 1)
elif  a==100:
    contador_metal = max(0, contador_metal - 1)

print(contador_plastico)