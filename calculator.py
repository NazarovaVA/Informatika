import sys
import re
pattern1=r'^([A-Z0-9]+ . )+[A-Z0-9]+$'
# Функция для сложения двух элементов (n1,n2 - массивы с int-элементами)
def plus(n1,n2):
    if len(n1)>len(n2):
        n2=[0]*(len(n1)-len(n2))+n2
    elif len(n1)<len(n2):
        n1=[0]*(len(n2)-len(n1))+n1
    n1=[0]+n1
    n2=[0]+n2
    n3=[]
    for i in range(len(n2)-1,-1,-1):
        if n1[i]+n2[i]>=ss:
            n3.append(n1[i]+n2[i]-ss)
            n1[i-1]=n1[i-1]+1
        else:
            n3.append(n1[i]+n2[i])
    if n3[-1]==0:
        n3=n3[:-1]
    return n3[::-1]

# Функция для вычитания двух элементов (n1,n2 - массивы с int-элементами)
def minus(n1,n2):
    if len(n1)>len(n2):
        n2=[0]*(len(n1)-len(n2))+n2
    n1=[0]+n1
    n2=[0]+n2
    n3=[]
    for i in range(len(n1)-1,-1,-1):
        if n1[i]-n2[i]<0:
            n3.append(n1[i]-n2[i]+ss)
            n1[i-1]=n1[i-1]-1
        else:
            n3.append(n1[i]-n2[i])
    if n3[-1]==0:
        n3=n3[:-1]
    return n3[::-1]

# Функция для умножения двух элементов (n1,n2 - массивы с int-элементами)
def multiplication(n1,n2):
    if len(n2)>len(n1):
        n1,n2=n2,n1
    sums=[]
    for i in range(len(n2)-1,-1,-1):
        sums.append(m(n1,n2[i]))
        sums.append('+')
    if sums[-1]=='+':
        sums=sums[:-1]
    k=0
    for i in range(1,len(sums),2):
        if str((sums[i])[0]) in '+-*':
            if (sums[i])[0]=='+':
                k+=1
                a=plus(sums[i-1],sums[i+1]+[0]*k)
            sums[i+1]=a
            sums[i-1],sums[i]=[0],[0]
    return sums[-1]

# Вспомогательная функция для умножения (n1-массив с int-элементами, n2-число)
def m(n1,n2): 
    n1=[0]+n1
    n3=[]
    t=0
    for i in range(len(n1)-1,-1,-1):
        if n1[i]*n2+t>=ss:
            n3.append((n1[i]*n2+t)%ss)
        else:
            n3.append(n1[i]*n2+t)
        t=(n1[i]*n2+t)//ss
    return n3[::-1]

#Убираем лишние [0] из массива
def preparing(s):
    res=[]
    for i in s:
        if i!=[0]:
            res=res + [i]
    return res

#Проверка, что первое число больше второго
def verify(n1,n2): 
    if len(n1)>len(n2) or n1==n2:
        return 1
    elif len(n1)<len(n2):
        return 0
    else:
        for i in range(len(n1)):
            if n1[i]>n2[i]:
                return 1
            elif n1[i]<n2[i]:
                return 0

#Проверка, что число соответствует заданной сс
def validnum(s):
    t=[]
    for i in range(0,len(s),2):
        if type(s[i])==int:
            if i>=ss:
                t.append(i)
        else:
            for r in s[i]:
                if r>=ss:
                    t.append(r)
    if t:
        return alf_reverse(t)
    else:
        return t
     
#Перевод для систем счисления, основание которых больше 9 + перевод элементов чисел в int
def alf_and_int(s):
    alf='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in s: #Для каждого числа в строке 
        for r in i: #Для каждой цифры числа
            e=i.index(r) #Находим индекс первого вхождения элемента (чтобы потом поменять его)
            if r in alf: #Если элемент - это буква
                i[e]=(alf.index(r))+10 #то меняем на число
            elif r in '0123456789':
                i[e]=int(r)
    return s
#перевод цифр больше 9 в буквы для правильности ответа
def alf_reverse(prevres):
    alf='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    res=''
    for i in range(len(prevres)):
        if prevres[i]>9:
            prevres[i]=alf[prevres[i]-10]
        res=res+str(prevres[i])
    return res

#Конечный перевод цифр больше 9 в буквы для правильности ответа
def alf_reverse_end(s):
    alf='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    prevres=(preparing(s)[0])
    res=''
    for i in range(len(prevres)):
        if prevres[i]>9:
            prevres[i]=alf[prevres[i]-10]
        res=res+str(prevres[i])
    if res.count('0')==len(res):
        return 0 
    else:
        return res
        
#Начало
ss=input("Введите систему счисления (до 36 включительно): ")
#Проверка правильности введения системы счисления
if ss in [str(x) for x in range(2,37)]:
    ss=int(ss)
else:
    sys.exit("Неверное значение системы счисления")
p=input("Введите арифметическое выражение, отделяя каждый знак(+-*) пробелом с двух сторон: ")
#Проверка на допустимость арифметического выражения
if re.match(pattern1,p):
    p=p.split()
else:
    sys.exit(f'Вы ввели недопустимое арифметическое выражение, проверьте, что все буквы заглавные и латинские, что знаки отделены пробелами и что выражение корректно')
#Разделяем числа в массиве на мини-массивы, чтобы каждый элемент каждого числа был отделён
s=[]
for i in p:
    s.append(list(map(str,i)))
#Перевод цифр больше 9 в буквы и цифр меньше 9 в int-элементы
s=alf_and_int(s)
#Проверка на соответствие чисел системе счисления
v=validnum(s)
if v:
    sys.exit(f'Вы ввели недопустимые числа для {ss}-ричной сс: {v} ')

#Первым делаем умножение (как в математике)
for i in range(1,len(s),2):
    if str((s[i])[0]) in '*':
        if s[i-1]==[1] or s[i+1]==[1]:
            if s[i+1]==[1]:
                s[i+1]=s[i-1]
            s[i-1],s[i]=[0],[0]
        else:
            a=multiplication(s[i-1],s[i+1])
            s[i+1]=a
            s[i-1],s[i]=[0],[0]
        #Убираем ненужные нули
        s=preparing(s)

#Считываем + и - и вызываем функции к ним
for i in range(1,len(s),2):
    if str((s[i])[0]) in '+-':
        if (s[i])[0]=='+':
            if s[i-1]==[0] or s[i+1]==[0]:
                if s[i+1]==[0]:
                    s[i+1]=s[i-1]
                s[i-1],s[i]=[0],[0]
            else:
                a=plus(s[i-1],s[i+1])
                s[i+1]=a
                s[i-1],s[i]=[0],[0]
        else:
            #Условие, что разность >=0
            if verify(s[i-1],s[i+1]):
                a=minus(s[i-1],s[i+1])
                s[i+1]=a
                s[i-1],s[i]=[0],[0]
            else:
                sys.exit('При вычитании получилось число меньше нуля, такое мы решить пока не можем :(')
    else:
        sys.exit(f'Вы ввели недопустимый знак действия, можно вводить только +-*')

#Вывод результата, в котором заменены числа больше 9 на буквы
print(f'Результат: {alf_reverse_end(s)}')