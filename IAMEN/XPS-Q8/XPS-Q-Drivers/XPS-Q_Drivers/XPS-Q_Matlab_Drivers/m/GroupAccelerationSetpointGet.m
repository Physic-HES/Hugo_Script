function [errorCode, SetpointAcceleration] = GroupAccelerationSetpointGet(socketId, GroupName, nbElement)
%GroupAccelerationSetpointGet :  Return setpoint accelerations
%
%	[errorCode, SetpointAcceleration] = GroupAccelerationSetpointGet(socketId, GroupName, nbElement)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		int32 nbElement
%	* Output parameters :
%		int32 errorCode
%		doublePtr SetpointAcceleration


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
SetpointAcceleration = [];
for i = 1:nbElement
	SetpointAcceleration = [SetpointAcceleration 0];
end

% lib call
[errorCode, GroupName, SetpointAcceleration] = calllib('XPS_Q8_drivers', 'GroupAccelerationSetpointGet', socketId, GroupName, nbElement, SetpointAcceleration);
