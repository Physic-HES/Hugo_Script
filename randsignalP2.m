function x0=randsignalP2(M1,tiem,Fs)
[FileName,Patch]=uiputfile({'*.txt'},'Guardar');
if Fs<2*max(M1(:,1));
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
for k=2:length(M(:,1));
    f=(M(k-1,1):F(2):M(k,1))';
    amp1=exp((log(M(k,2))-log(M(k-1,2)))/(log(M(k,1))-log(M(k-1,1))).*(log(f)-log(M(k-1,1)))+log(M(k-1,2)));
    amp=[amp;amp1];
end
amp=[amp;zeros(length(t)-length(amp),1)];
noise=randn(length(amp)*2,1);
temp=real(ifft(amp.*noise(1:end/2),'symmetric'));
temp=temp*norm(amp*sqrt(F(2)))/norm(temp)*sqrt(length(temp));
x0=[t' temp(1:length(t))];
dlmwrite([Patch FileName],x0,'delimiter','\t','precision','%2.6f');
disp(sprintf('RMS_temp: %g',norm(x0(:,2))/sqrt(length(x0(:,2)))))
plot(x0(:,1),x0(:,2));
xlabel('Time [sec]'); ylabel('Acceleration [G]'); xlim([0 max(t)]); grid on;
title(sprintf('History of Acceleration Random Signal %2.1f Grms',norm(x0(:,2))/sqrt(length(x0(:,2)))));
figure;
[Mfft,fac]=fespectrohw321(x0,F,amp);
Mfft(:,2)=Mfft(:,2)*norm(amp*sqrt(F(2)))/norm(fac(2)*abs(Mfft(:,2))/sqrt(2));
disp(sprintf('RMS_fft: %g',norm(fac(2)*abs(Mfft(:,2))/sqrt(2))))
end
