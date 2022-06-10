function [errorCode, SetPointPosition] = GroupPositionSetpointGet(socketId, GroupName, nbElement)
%GroupPositionSetpointGet :  Return setpoint positions
%
%	[errorCode, SetPointPosition] = GroupPositionSetpointGet(socketId, GroupName, nbElement)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		int32 nbElement
%	* Output parameters :
%		int32 errorCode
%		doublePtr SetPointPosition


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
SetPointPosition = [];
for i = 1:nbElement
	SetPointPosition = [SetPointPosition 0];
end

% lib call
[errorCode, GroupName, SetPointPosition] = calllib('XPS_Q8_drivers', 'GroupPositionSetpointGet', socketId, GroupName, nbElement, SetPointPosition);
