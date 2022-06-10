function [errorCode, ReturnString] = TestTCP(socketId, InputString)
%TestTCP :  Test TCP/IP transfert
%
%	[errorCode, ReturnString] = TestTCP(socketId, InputString)
%
%	* Input parameters :
%		int32 socketId
%		cstring InputString
%	* Output parameters :
%		int32 errorCode
%		cstring ReturnString


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
ReturnString = '';
for i = 1:103
	ReturnString = [ReturnString '          '];
end

% lib call
[errorCode, InputString, ReturnString] = calllib('XPS_Q8_drivers', 'TestTCP', socketId, InputString, ReturnString);
