function [errorCode, CurrentVelocity] = GroupVelocityCurrentGet(socketId, GroupName, nbElement)
%GroupVelocityCurrentGet :  Return current velocities
%
%	[errorCode, CurrentVelocity] = GroupVelocityCurrentGet(socketId, GroupName, nbElement)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		int32 nbElement
%	* Output parameters :
%		int32 errorCode
%		doublePtr CurrentVelocity


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
CurrentVelocity = [];
for i = 1:nbElement
	CurrentVelocity = [CurrentVelocity 0];
end

% lib call
[errorCode, GroupName, CurrentVelocity] = calllib('XPS_Q8_drivers', 'GroupVelocityCurrentGet', socketId, GroupName, nbElement, CurrentVelocity);
