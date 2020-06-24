while True:
	s= str(input('Сумма: '))
	s=s.replace(' ','')
	s=int(s)
	if s==0:
		break
	p=float(input('Процент: '))
	k=int(input('Кол-во месяцев: '))
	for i in range(k):
		s=s+(p/1200)*s
	print('Результат:',round(s,2),'руб.')
	print("=============")