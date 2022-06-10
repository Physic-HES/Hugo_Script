function [errorCode, CurrentEncoderPosition] = GroupPositionCurrentGet(socketId, GroupName, nbElement)
%GroupPositionCurrentGet :  Return current positions
%
%	[errorCode, CurrentEncoderPosition] = GroupPositionCurrentGet(socketId, GroupName, nbElement)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		int32 nbElement
%	* Output parameters :
%		int32 errorCode
%		doublePtr CurrentEncoderPosition


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
CurrentEncoderPosition = [];
for i = 1:nbElement
	CurrentEncoderPosition = [CurrentEncoderPosition 0];
end

% lib call
[errorCode, GroupName, CurrentEncoderPosition] = calllib('XPS_Q8_drivers', 'GroupPositionCurrentGet', socketId, GroupName, nbElement, CurrentEncoderPosition);
