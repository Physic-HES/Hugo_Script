function [errorCode, TargetPosition] = GroupPositionTargetGet(socketId, GroupName, nbElement)
%GroupPositionTargetGet :  Return target positions
%
%	[errorCode, TargetPosition] = GroupPositionTargetGet(socketId, GroupName, nbElement)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		int32 nbElement
%	* Output parameters :
%		int32 errorCode
%		doublePtr TargetPosition


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
TargetPosition = [];
for i = 1:nbElement
	TargetPosition = [TargetPosition 0];
end

% lib call
[errorCode, GroupName, TargetPosition] = calllib('XPS_Q8_drivers', 'GroupPositionTargetGet', socketId, GroupName, nbElement, TargetPosition);
