import random
import scipy.stats as stats

ran_list = []

n = 1000

for i in range(n) :
    x = random.random()
    ran_list.append(x)

k = 10
interval_list = [0 for i in range(k)]


for i in ran_list :
    for j in range(k) :
        if j/k <= i < (j+1)/k :
            interval_list[j] += 1

sigma = 0

for i in range(k) :
    sigma += (interval_list[i]-n/k)*(interval_list[i]-n/k)

stat = (k/n)*sigma

crit = stats.chi2.ppf(q = 0.95, df = k-1)

print("H0 : Ui are IID U(0,1) random variables.")
print("H1 : Ui are not IID U(0,1) random variables.")
print("Test statistic : "+str(stat))
print("Critical value : "+str(crit))
if stat > crit :
    print("Reject H0 at a=0.05. Ui are not IID U(0,1) random variables.")
else :
    print("Do not reject H0 at a=0.05. There is no significant evidence to conclude that Ui are not IID U(0,1) random variables.")

file = open("Chi-square test result.txt", 'w')

file.write("H0 : Ui are IID U(0,1) random variables.\n")
file.write("H1 : Ui are not IID U(0,1) random variables.\n\n")
file.write("Test statistic : "+str(stat))
file.write("\nCritical value : "+str(crit))
if stat > crit :
    file.write("\n\nReject H0 at a=0.05. Ui are not IID U(0,1) random variables.")
else :
    file.write("\n\nDo not reject H0 at a=0.05. There is no significant evidence to conclude that Ui are not IID U(0,1) random variables.")


file.close()

