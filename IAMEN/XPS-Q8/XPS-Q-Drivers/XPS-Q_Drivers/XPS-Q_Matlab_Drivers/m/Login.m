function [errorCode] = Login(socketId, Name, Password)
%Login :  Log in
%
%	[errorCode] = Login(socketId, Name, Password)
%
%	* Input parameters :
%		int32 socketId
%		cstring Name
%		cstring Password
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, Name, Password] = calllib('XPS_Q8_drivers', 'Login', socketId, Name, Password);
