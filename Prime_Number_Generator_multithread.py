from multiprocessing import Pool,Process
from numba import jit

#global past_prime_numbers
#global global_New_prime

file= open("Prime_Numbers.txt","r")
past_prime_numbers=file.read().split(',')
file.close()
del file

    
#@jit(nopython=True)
def str_to_int(past_prime_numbers):
    for I in range(len(past_prime_numbers)):
        past_prime_numbers[I]=int(past_prime_numbers[I])
    return past_prime_numbers


past_prime_numbers=str_to_int(past_prime_numbers)

file=open("Prime_Numbers.txt","a")

@jit(nopython=True,fastmath=True)
def New_Prime_number_test(New_Prime_Number,past_prime_numbers, Max):
    number=0
    total=0
    New_Prime_Numbers=[0]* round_down(Max-(New_Prime_Number-1)/2)
    
    while New_Prime_Number < Max:
        if New_Prime_Number%past_prime_numbers[number]==0:
            New_Prime_Number+=1
            number=0
        else:
            if past_prime_numbers[number]<=New_Prime_Number/4:
                number+=1
            else:
                New_Prime_Numbers[total]=New_Prime_Number
                total+=1
                New_Prime_Number+=1
                number=0
                
    return New_Prime_Numbers
                
@jit(nopython=True,fastmath=True)
def remove_zero(array):
    if array==0:
        return False
    return True

@jit(nopython=True,fastmath=True)
def round_down(start_number):
    number_1=round(start_number)
    if number_1>start_number:
        number_1=number_1-1
    return number_1

#round down
thread_alocation=1
Main_Thread=True            
threads = [None] * thread_alocation
#work= [None] * thread_alocation

if __name__ == '__main__':
    while Main_Thread:
        len_past_prime_number=len(past_prime_numbers)-1
        Max=past_prime_numbers[len_past_prime_number]*4
        New_Prime_Number=past_prime_numbers[len_past_prime_number]+1

        print(New_Prime_Number)    
        total=(Max-New_Prime_Number)
        per_thread=round_down(total/thread_alocation)
        rem=total%thread_alocation

        for I in range(thread_alocation):
            start=New_Prime_Number+(per_thread*I)
            end=start+ per_thread
            if I==thread_alocation-1:
                end+=rem
            threads[I]= Process (target=New_Prime_number_test,args=(start,past_prime_numbers,end,))
            threads[I].start()
        
        for I in range(thread_alocation):
            data=list(filter(remove_zero,threads[I].join()))
            for I in range(len(data)):
                file.write(","+str(data[I]))
            past_prime_numbers.extend(data)    
        
        
        #print(past_prime_numbers)
    
          
file.close()