from multiprocessing import Pool,Process
from numba import jit
import time

file= open("Prime_Numbers1.txt","r")
past_prime_numbers=file.read().split(',')
file.close()
del file

#@jit(nopython=True)
def str_to_int(past_prime_numbers):
    for I in range(len(past_prime_numbers)):
        past_prime_numbers[I]=int(past_prime_numbers[I])
    return past_prime_numbers

past_prime_numbers=str_to_int(past_prime_numbers)

file=open("Prime_Numbers1.txt","a")

@jit(nopython=True,fastmath=True,cache=True)
def New_Prime_number_test(New_Prime_Number,past_prime_numbers, Max):
    number=0
    New_Prime_Numbers=[]
    while New_Prime_Number < Max:
        if New_Prime_Number%past_prime_numbers[number]==0:
            New_Prime_Number+=2
            number=0
        else:
            if past_prime_numbers[number]<=New_Prime_Number/4:
                number+=1
            else:
                New_Prime_Numbers.append(New_Prime_Number)
                New_Prime_Number+=2
                number=0
                
    return New_Prime_Numbers

@jit(nopython=True,fastmath=True,cache=True)
def round_down(start_number):
    number_1=round(start_number)
    if number_1>start_number:
        number_1=number_1-1
    return number_1

#round down
thread_alocation=24
Main_Thread=True            
threads = [None] * thread_alocation

if __name__ == '__main__':
    while Main_Thread:
        start_time=time.time()
        len_past_prime_number=len(past_prime_numbers)-1
        Max=past_prime_numbers[len_past_prime_number]*4
        New_Prime_Number=past_prime_numbers[len_past_prime_number]

        print(New_Prime_Number, Max)
        #print(Max-New_Prime_Number)
        
        total=(Max-New_Prime_Number)
        per_thread=round_down(total/thread_alocation)
        rem=total%thread_alocation

        pool=Pool(processes=thread_alocation)
        for I in range(thread_alocation):
            start=New_Prime_Number+(per_thread*I)
            end=start+ per_thread
            if I==thread_alocation-1:
                end+=rem
            #print(start,end)
            threads[I]= pool.apply_async(New_Prime_number_test,args=(start,past_prime_numbers[:end],end,))
        for I in range(thread_alocation):
            data=threads[I].get()
            #for I in range(len(data)):
            #    file.write(","+str(data[I]))
            past_prime_numbers.extend(data)
            
        """for I in range(thread_alocation):
            data=list(filter(remove_zero,threads[I].join()))
            for I in range(len(data)):
                file.write(","+str(data[I]))
            past_prime_numbers.extend(data)"""    

        print(len(past_prime_numbers))
        print(time.time()-start_time)
        break
    
          
file.close()
