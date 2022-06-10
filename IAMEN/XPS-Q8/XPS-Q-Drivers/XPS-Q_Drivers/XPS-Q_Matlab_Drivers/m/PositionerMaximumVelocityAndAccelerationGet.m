function [errorCode, MaximumVelocity, MaximumAcceleration] = PositionerMaximumVelocityAndAccelerationGet(socketId, PositionerName)
%PositionerMaximumVelocityAndAccelerationGet :  Return maximum velocity and acceleration of the positioner
%
%	[errorCode, MaximumVelocity, MaximumAcceleration] = PositionerMaximumVelocityAndAccelerationGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr MaximumVelocity
%		doublePtr MaximumAcceleration


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
MaximumVelocity = 0;
MaximumAcceleration = 0;

% lib call
[errorCode, PositionerName, MaximumVelocity, MaximumAcceleration] = calllib('XPS_Q8_drivers', 'PositionerMaximumVelocityAndAccelerationGet', socketId, PositionerName, MaximumVelocity, MaximumAcceleration);
