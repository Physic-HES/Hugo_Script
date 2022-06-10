function [errorCode, ElapsedTime] = ElapsedTimeGet(socketId)
%ElapsedTimeGet :  Return elapsed time from controller power on
%
%	[errorCode, ElapsedTime] = ElapsedTimeGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		doublePtr ElapsedTime


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
ElapsedTime = 0;

% lib call
[errorCode, ElapsedTime] = calllib('XPS_Q8_drivers', 'ElapsedTimeGet', socketId, ElapsedTime);
