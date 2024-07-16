function x0=randsignalP2(M1,tiem,Fs)

% Genera una señal temporal que contiene la composicion en frecuencia requerida en M1 
% suponiendo una fase aleatoria para cada componente, y rampas de M1 lineales en doble logaritmico.

% Parametros de entrada:

% M1 <- es una matriz con los puntos en donde cambia el SRS o spec de requerimiento 
% que se introduzca como input, en la que la primer columna corresponde a la
% frecuencia y la segunta a la amplitud.
%
% tiem <- es el tiempo de temporal que uno quiere obtener
%
% Fs <- la frecuencia de muestreo que uno quiere que tenga la temporal (delta t =1/Fs)

% Parametros de salida:

% x0 <- es una matriz de salida que contiene en la primer columna el tiempo y
% en la segunda la señal obtenida

% El codigo tambien plotea un Power Spectum en doble logaritmico para que
% se corrobore que coincide con la spec del requerimiento.


[FileName,Patch]=uiputfile({'*.txt'},'Guardar');
if Fs<2*max(M1(:,1))
    warning('Muestreo por debajo de Nysquit, \n las ultimas componentes pueden atenuarse');
elseif tiem<1/min(M1(:,1))
    warning('Duracion por debajo de Nysquit, \n las primeras componentes pueden atenuarse');
end
t=tiem*linspace(0,1,tiem*Fs);
F=linspace(0,Fs,length(t))';
M(:,1)=M1(:,1);
M(:,2)=sqrt(M1(:,2));
ini=find(abs(F-M(1,1))<(F(2)-F(1))/2);
amp=zeros(size(F(1:ini-1,1)));
for k=2:length(M(:,1))
    f=(M(k-1,1):F(2):M(k,1))';
    amp1=exp((log(M(k,2))-log(M(k-1,2)))/(log(M(k,1))-log(M(k-1,1))).*(log(f)-log(M(k-1,1)))+log(M(k-1,2)));
    amp=[amp;amp1];
end
amp=[amp;zeros(length(t)-length(amp),1)];
noise=randn(length(amp),1);
temp=real(ifft(amp.*exp(1i*2*pi*(linspace(0,Fs,length(amp))'+noise)),'symmetric'));
temp=2*temp*norm(amp*sqrt(F(2)))/norm(temp)*sqrt(length(temp));
x0=[t' temp(1:length(t))];
dlmwrite([Patch FileName],x0,'delimiter','\t','precision','%2.6f');
fprintf('RMS_temp: %g\n',norm(x0(:,2))/sqrt(length(x0(:,2))))
plot(x0(:,1),x0(:,2));
xlabel('Time [sec]'); ylabel('Acceleration [G]'); xlim([0 max(t)]); grid on;
title(sprintf('History of Acceleration Signal - %2.1f Grms',norm(x0(:,2))/sqrt(length(x0(:,2)))));
figure;
[Y,f]=pspectrum(x0(:,2),Fs);
loglog(f,Y)
ylabel('EU: 0-pk amp')
xlabel('Frequency [Hz]')
end
