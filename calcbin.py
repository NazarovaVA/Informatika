import sys
import re
pattern1=r'^(((-?([1-9])+[0-9]*)|0) . )+((-?([1-9])+[0-9]*)|0)$'

#Проверка на переролнение
def verify(r1,r2,r3,z):
    if r3 <-128 or r3>127:
        return sys.exit("Переполнение при выполнении арифметической операции")
    if z == "+":
        if r1 > 0 and r2 > 0 and r3 < 0:
            return sys.exit("Переполнение при выполнении арифметической операции")
        elif r1 < 0 and r2 < 0 and r3 > 0:
            return sys.exit("Переполнение при выполнении арифметической операции")
    elif z == "*":
        if (r1 > 0 and r2 > 0 and r3 < 0) or (r1 < 0 and r2 < 0 and r3 < 0):
            return sys.exit("Переполнение при выполнении арифметической операции")
        elif (r1 > 0 and r2 < 0 and r3 > 0) or (r1 < 0 and r2 > 0 and r3 > 0):
            return sys.exit("Переполнение при выполнении арифметической операции")
    
#Перевод в 10сс
def reversedk(n):
    a=n[0]
    if a==0:
        return int("".join([str(x) for x in n[1:]]),2)
    else:
        n1=n[1:]
        n2='0000001'
        n3=[]
        for i in range(len(n1)-1,-1,-1):
            if n1[i]-int(n2[i])<0:
                n3.append(n1[i]-int(n2[i])+2)
                n1[i-1]=n1[i-1]-1
            else:
                n3.append(n1[i]-int(n2[i]))
        n3=n3[::-1]
        n="".join([str(x) for x in n3])
        n=n.replace('0','2')
        n=n.replace('1','0')
        n=n.replace('2','1')
        n=str(int(n,2))
        if a==1:
            n='-'+n
        return int(n)

#Уборка ненужных нулей
def preparing(s):
    res=[]
    for i in s:
        if i!=[0]:
            res=res + [i]
    return res

#Перевод в дополнительный код
def dk(n):
    num=n
    if 127>=int(n)>=0:
        n=bin(int(n))[2:]
        #Прямой, обратный и дополнительный код для неотрицательного числа
        n='0'*(8-len(n))+n
        print(f'Дополнительный код числа {num}: {n}')
    elif int(n)>127 or int(n)<-128:
        sys.exit("Переполнение при переводе в дополнительный код")
    elif int(n)==-128:
        n='10000000'
        print(f'Дополнительный код числа {num}: {n}')
    else:
        n=bin(-int(n))[2:]
        #Прямой код
        n='1'+'0'*(7-len(n))+n
        #Обратный код
        n1=n[0]
        n=n[1:]
        n=n.replace('1','2')
        n=n.replace('0','1')
        n=n.replace('2','0')
        n=n1+n
        n=[x for x in n]
        #Дополнительный код
        n2='00000001'
        n3=''
        for i in range(len(n)-1,-1,-1):
            if int(n2[i])+int(n[i])>=2:
                n3=str(int(n2[i])+int(n[i])-2)+n3
                n[i-1]=str(int(n[i-1])+1)
            else:
                n3=str(int(n2[i])+int(n[i]))+n3
        n=n3
        print(f'Дополнительный код числа {num}: {n}')
    return n

#Сложение
def plus(n1,n2):
    n1,n2=n1[len(n1)-8:],n2[len(n2)-8:]
    x1,x2="".join([str(x) for x in n1]),"".join([str(x) for x in n2])
    n3=[]
    r1,r2 = reversedk(n1),reversedk(n2)
    for i in range(len(n1)-1,-1,-1):
        if n1[i]+n2[i]>=2:
            n3.append(n1[i]+n2[i]-2)
            n1[i-1]=n1[i-1]+1
        else:
            n3.append(n1[i]+n2[i])
    n3=n3[::-1]
    x3="".join([str(x) for x in n3])
    r3 = reversedk(n3)
    verify(r1,r2,r3,"+")
    print(f"Промежуточный шаг: {x1} + {x2} = {x3}")
    return n3

#Сложение для умножения
def plus_for_multipl(n1,n2):
    n1,n2=n1[len(n1)-8:],n2[len(n2)-8:]
    n3=[]
    r1,r2 = reversedk(n1),reversedk(n2)
    for i in range(len(n1)-1,-1,-1):
        if n1[i]+n2[i]>=2:
            n3.append(n1[i]+n2[i]-2)
            n1[i-1]=n1[i-1]+1
        else:
            n3.append(n1[i]+n2[i])
    n3=n3[::-1]
    r3 = reversedk(n3)
    verify(r1,r2,r3,"+")
    return n3

#Умножение
def multiplication(n1,n2):
    r1,r2 = reversedk(n1),reversedk(n2)
    x1,x2="".join([str(x) for x in n1]),"".join([str(x) for x in n2])
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
                a=plus_for_multipl(sums[i-1],sums[i+1]+[0]*k)
            sums[i+1]=a
            sums[i-1],sums[i]=[0]*8,[0]*8
    sums=sums[-1]
    x3="".join([str(x) for x in sums])
    r3=reversedk(sums)
    verify(r1,r2,r3,"*")
    print(f'Промежуточный шаг: {x1} * {x2} = {x3}')
    return sums

# Вспомогательная функция для умножения
def m(n1,n2): 
    n1=[0]+n1
    n3=[]
    t=0
    for i in range(len(n1)-1,-1,-1):
        if n1[i]*n2+t>=2:
            n3.append((n1[i]*n2+t)%2)
        else:
            n3.append(n1[i]*n2+t)
        t=(n1[i]*n2+t)//2
    return n3[::-1]

#Начало
p=input("Введите арифметическое выражение, отделяя каждый знак действия(+-*) пробелом с двух сторон (если число <0, то отделять '-' не надо, он является частью числа): ")
#Проверка на допустимость арифметического выражения
if re.match(pattern1,p):
    p=p.split()
else:
    sys.exit(f'Вы ввели недопустимое арифметическое выражение, проверьте, что все буквы заглавные и латинские, что знаки отделены пробелами и что выражение корректно')

#Преобразовываем выражение
w=0
for i in range(len(p)-1):
    if p[i]=='-' and (p[i+1])[0]=='-':
        p[i]='+'
        p[i+1]=(p[i+1])[1:]
        w=1
    elif p[i]=='-':
        p[i]='+'
        p[i+1]='-'+p[i+1]
        w=1
    elif p[i]=='+':
        if (p[i-1])[0]=='-' and (p[i+1][0])!='-':
            p[i-1],p[i+1]=p[i+1],p[i-1]
            w=1
    elif p[i]=='*':
        if (p[i+1])[0]=='-' and (p[i-1])[0]!='-':
            p[i-1],p[i+1]=p[i+1],p[i-1]
            w=1
#Выводим выражение, если оно хотя бы как-то изменилось
if w==1:
    print(f'Преобразованное выражение: {" ".join(p)}')

#Перевод в доп. код
s=[]
for i in p:
    if i in '+-*':
        s.append(i)
    else:
        s.append(dk(i))
#Вывод нового выражения
print(f'Арифметическое выражение в машинном представлении: {" ".join(s)}')


#Разделяем каждый доп. код на цифры
p=[]
for i in s:
    r=[]
    for e in i:
        if e in '+-*':
            r.append(e)
        else:
            r.append(int(e))
    p.append(r)
s=p
#Первым делаем умножение (как в математике)
for i in range(1,len(s),2):
    if str((s[i])[0]) in '*':
        a=multiplication(s[i-1],s[i+1])
        s[i+1]=a
        s[i-1],s[i]=[0],[0]
#Уборка ненужных нулей
s=preparing(s)
#Сложение
for i in range(1,len(s),2):
    if str((s[i])[0]) in '+':
        a=plus(s[i-1],s[i+1])
        s[i+1]=a
        s[i-1],s[i]=[0]*8,[0]*8
    else:
        sys.exit(f'Вы ввели недопустимый знак действия, можно вводить только +-*')
#Выделение ответа
ans = s[-1]
print(f'Итоговый результат в дополнительном коде: {"".join([str(x) for x in ans])}')
print(f'Итоговый результат в 10 сс: {reversedk(ans)}')