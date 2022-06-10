function [errorCode, StagePositionOffset, GagePositionOffset] = PositionerDriverPositionOffsetsGet(socketId, PositionerName)
%PositionerDriverPositionOffsetsGet :  Get driver stage and gage position offset
%
%	[errorCode, StagePositionOffset, GagePositionOffset] = PositionerDriverPositionOffsetsGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr StagePositionOffset
%		doublePtr GagePositionOffset


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
StagePositionOffset = 0;
GagePositionOffset = 0;

% lib call
[errorCode, PositionerName, StagePositionOffset, GagePositionOffset] = calllib('XPS_Q8_drivers', 'PositionerDriverPositionOffsetsGet', socketId, PositionerName, StagePositionOffset, GagePositionOffset);
