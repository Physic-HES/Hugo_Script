function [errorCode] = PositionerCorrectorPIDBaseSet(socketId, PositionerName, MovingMass, StaticMass, Viscosity, Stiffness)
%PositionerCorrectorPIDBaseSet :  Update PIDBase parameters 
%
%	[errorCode] = PositionerCorrectorPIDBaseSet(socketId, PositionerName, MovingMass, StaticMass, Viscosity, Stiffness)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double MovingMass
%		double StaticMass
%		double Viscosity
%		double Stiffness
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_C8_drivers', 'PositionerCorrectorPIDBaseSet', socketId, PositionerName, MovingMass, StaticMass, Viscosity, Stiffness);
