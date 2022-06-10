function [errorCode] = GatheringReset(socketId)
%GatheringReset :  Empty the gathered data in memory to start new gathering from scratch
%
%	[errorCode] = GatheringReset(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode] = calllib('XPS_Q8_drivers', 'GatheringReset', socketId);
