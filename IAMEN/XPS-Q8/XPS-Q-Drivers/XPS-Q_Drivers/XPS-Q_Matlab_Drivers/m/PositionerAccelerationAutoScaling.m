function [errorCode, Scaling] = PositionerAccelerationAutoScaling(socketId, PositionerName)
%PositionerAccelerationAutoScaling :  Astrom&Hagglund based auto-scaling
%
%	[errorCode, Scaling] = PositionerAccelerationAutoScaling(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr Scaling


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
Scaling = 0;

% lib call
[errorCode, PositionerName, Scaling] = calllib('XPS_Q8_drivers', 'PositionerAccelerationAutoScaling', socketId, PositionerName, Scaling);
