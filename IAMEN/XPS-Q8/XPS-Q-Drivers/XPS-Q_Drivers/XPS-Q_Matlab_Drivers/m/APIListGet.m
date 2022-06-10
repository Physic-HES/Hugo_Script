function [errorCode, Method] = APIListGet(socketId)
%APIListGet :  API method list without extended API
%
%	[errorCode, Method] = APIListGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		cstring Method


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
Method = '';
for i = 1:6554
	Method = [Method '          '];
end

% lib call
[errorCode, Method] = calllib('XPS_Q8_drivers', 'APIListGet', socketId, Method);
