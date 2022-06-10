function [errorCode] = KillAll(socketId)
%KillAll :  Put all groups in 'Not initialized' state
%
%	[errorCode] = KillAll(socketId)
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
[errorCode] = calllib('XPS_Q8_drivers', 'KillAll', socketId);
