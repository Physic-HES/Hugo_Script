function [errorCode, MinimumPosition, MaximumPosition, PositionStep, EnableState] = PositionerPositionCompareGet(socketId, PositionerName)
%PositionerPositionCompareGet :  Read position compare parameters
%
%	[errorCode, MinimumPosition, MaximumPosition, PositionStep, EnableState] = PositionerPositionCompareGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr MinimumPosition
%		doublePtr MaximumPosition
%		doublePtr PositionStep
%		int16Ptr EnableState


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
MinimumPosition = 0;
MaximumPosition = 0;
PositionStep = 0;
EnableState = 0;

% lib call
[errorCode, PositionerName, MinimumPosition, MaximumPosition, PositionStep, EnableState] = calllib('XPS_Q8_drivers', 'PositionerPositionCompareGet', socketId, PositionerName, MinimumPosition, MaximumPosition, PositionStep, EnableState);
