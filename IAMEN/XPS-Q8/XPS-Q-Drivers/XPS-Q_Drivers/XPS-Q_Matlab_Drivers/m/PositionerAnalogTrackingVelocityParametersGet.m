function [errorCode, GPIOName, Offset, Scale, DeadBandThreshold, Order, Velocity, Acceleration] = PositionerAnalogTrackingVelocityParametersGet(socketId, PositionerName)
%PositionerAnalogTrackingVelocityParametersGet :  Read dynamic parameters for one axe of a group for a future analog tracking velocity
%
%	[errorCode, GPIOName, Offset, Scale, DeadBandThreshold, Order, Velocity, Acceleration] = PositionerAnalogTrackingVelocityParametersGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		cstring GPIOName
%		doublePtr Offset
%		doublePtr Scale
%		doublePtr DeadBandThreshold
%		int32Ptr Order
%		doublePtr Velocity
%		doublePtr Acceleration


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
GPIOName = '';
for i = 1:103
	GPIOName = [GPIOName '          '];
end
Offset = 0;
Scale = 0;
DeadBandThreshold = 0;
Order = 0;
Velocity = 0;
Acceleration = 0;

% lib call
[errorCode, PositionerName, GPIOName, Offset, Scale, DeadBandThreshold, Order, Velocity, Acceleration] = calllib('XPS_Q8_drivers', 'PositionerAnalogTrackingVelocityParametersGet', socketId, PositionerName, GPIOName, Offset, Scale, DeadBandThreshold, Order, Velocity, Acceleration);
