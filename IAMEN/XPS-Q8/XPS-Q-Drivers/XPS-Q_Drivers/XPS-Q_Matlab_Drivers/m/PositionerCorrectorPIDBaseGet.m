function [errorCode, MovingMass, StaticMass, Viscosity, Stiffness] = PositionerCorrectorPIDBaseGet(socketId, PositionerName)
%PositionerCorrectorPIDBaseGet :  Read PIDBase parameters 
%
%	[errorCode, MovingMass, StaticMass, Viscosity, Stiffness] = PositionerCorrectorPIDBaseGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr MovingMass
%		doublePtr StaticMass
%		doublePtr Viscosity
%		doublePtr Stiffness


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
MovingMass = 0;
StaticMass = 0;
Viscosity = 0;
Stiffness = 0;

% lib call
[errorCode, PositionerName, MovingMass, StaticMass, Viscosity, Stiffness] = calllib('XPS_C8_drivers', 'PositionerCorrectorPIDBaseGet', socketId, PositionerName, MovingMass, StaticMass, Viscosity, Stiffness);
