function [errorCode, distance] = PositionersEncoderIndexDifferenceGet(socketId, PositionerName)
%PositionersEncoderIndexDifferenceGet :  Return the difference between index of primary axis and secondary axis (only after homesearch)
%
%	[errorCode, distance] = PositionersEncoderIndexDifferenceGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr distance


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
distance = 0;

% lib call
[errorCode, PositionerName, distance] = calllib('XPS_Q8_drivers', 'PositionersEncoderIndexDifferenceGet', socketId, PositionerName, distance);
