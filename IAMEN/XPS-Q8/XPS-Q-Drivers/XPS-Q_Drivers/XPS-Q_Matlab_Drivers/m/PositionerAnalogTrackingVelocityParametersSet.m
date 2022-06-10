function [errorCode] = PositionerAnalogTrackingVelocityParametersSet(socketId, PositionerName, GPIOName, Offset, Scale, DeadBandThreshold, Order, Velocity, Acceleration)
%PositionerAnalogTrackingVelocityParametersSet :  Update dynamic parameters for one axe of a group for a future analog tracking velocity
%
%	[errorCode] = PositionerAnalogTrackingVelocityParametersSet(socketId, PositionerName, GPIOName, Offset, Scale, DeadBandThreshold, Order, Velocity, Acceleration)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		cstring GPIOName
%		double Offset
%		double Scale
%		double DeadBandThreshold
%		int32 Order
%		double Velocity
%		double Acceleration
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName, GPIOName] = calllib('XPS_Q8_drivers', 'PositionerAnalogTrackingVelocityParametersSet', socketId, PositionerName, GPIOName, Offset, Scale, DeadBandThreshold, Order, Velocity, Acceleration);
