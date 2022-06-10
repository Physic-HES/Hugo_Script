function [errorCode, MinimumPosition, MaximumPosition, EnableState] = PositionerPositionCompareAquadBWindowedGet(socketId, PositionerName)
%PositionerPositionCompareAquadBWindowedGet :  Read position compare AquadB windowed parameters
%
%	[errorCode, MinimumPosition, MaximumPosition, EnableState] = PositionerPositionCompareAquadBWindowedGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr MinimumPosition
%		doublePtr MaximumPosition
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
EnableState = 0;

% lib call
[errorCode, PositionerName, MinimumPosition, MaximumPosition, EnableState] = calllib('XPS_Q8_drivers', 'PositionerPositionCompareAquadBWindowedGet', socketId, PositionerName, MinimumPosition, MaximumPosition, EnableState);
