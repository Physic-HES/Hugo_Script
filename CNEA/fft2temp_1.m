function [M2,S1]=fft2temp_1(M,tiemp,Fs)
N=floor(tiemp*Fs);
[C,~,~]=union(M(:,1),M(:,1));
for j=1:length(C) 
    C(j,2)=mean(M(find(M(:,1)==C(j)),2)); 
end
M2(:,1)=linspace(min(M(:,1)),max(M(:,1)),N)';
M2(:,2)=interp1(C(:,1),C(:,2),linspace(min(M(:,1)),max(M(:,1)),N)');
transform=2*N*[M2(:,2);M2(sort(1:N,'descend'),2)]*1/2.*exp(2*pi*([M2(:,1);M2(:,1)+max(M2(:,1))]+rand(2*N,1))*i);
S=real(ifft(transform,'symmetric'));
S=S*norm(2*abs(transform(1:end/2))/(2*N)/sqrt(2))/(norm(S)/length(S))/N*sqrt(2);
S1(:,1)=linspace(0,tiemp,N);
S1(:,2)=S(1:N); 