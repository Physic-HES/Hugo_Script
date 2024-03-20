import pandas as pd
import matplotlib.pyplot as plt

# Sample data (replace with actual historical exchange rates)
dates = pd.date_range(start='2013-01-01', end='2024-02-01', freq='M')
camb=pd.read_csv('/home/hp1opticaiamend/Documents/USD_ARS Historical Data.csv')
Sueldo_CNEA=pd.read_csv('/home/hp1opticaiamend/Documents/Historico_salario_CNEA.csv',header=7)
exchange_rates = camb['Price'].values[::-1]

# Create a DataFrame
df = pd.DataFrame({'Date': dates, 'USD/ARS Exchange Rate': exchange_rates, 'Salario Bruto CNEA en ARG': Sueldo_CNEA['Remun.']})

print(df)
# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['USD/ARS Exchange Rate'], marker='o', linestyle='-', color='b')
plt.plot(df['Date'], 0.83*df['Salario Bruto CNEA en ARG'], marker='o', linestyle='-', color='r')
plt.title('Cambio USD/ARG y Salario Neto CNEA ARG (2013 - 2024)')
plt.xlabel('Date')
plt.ylabel('Pesos ARG')
plt.grid(True)

plt.figure(figsize=(10, 6))
plt.plot(df['Date'], 0.74/1.6*df['Salario Bruto CNEA en ARG']/df['USD/ARS Exchange Rate'], marker='o', linestyle='-', color='b')
plt.title('Salario Neto CNEA USD (2013 - 2024)')
plt.xlabel('Date')
plt.ylabel('Dolares USD')
plt.grid(True)
plt.show()
