function [errorCode] = GatheringRun(socketId, DataNumber, Divisor)
%GatheringRun :  Start a new gathering
%
%	[errorCode] = GatheringRun(socketId, DataNumber, Divisor)
%
%	* Input parameters :
%		int32 socketId
%		int32 DataNumber
%		int32 Divisor
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode] = calllib('XPS_Q8_drivers', 'GatheringRun', socketId, DataNumber, Divisor);
