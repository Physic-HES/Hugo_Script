function [errorCode, NotchModeFr1, NotchModeFa1, NotchModeZr1, NotchModeZa1, NotchModeFr2, NotchModeFa2, NotchModeZr2, NotchModeZa2] = PositionerCompensationNotchModeFiltersGet(socketId, PositionerName)
%PositionerCompensationNotchModeFiltersGet :  Read notch mode filters parameters 
%
%	[errorCode, NotchModeFr1, NotchModeFa1, NotchModeZr1, NotchModeZa1, NotchModeFr2, NotchModeFa2, NotchModeZr2, NotchModeZa2] = PositionerCompensationNotchModeFiltersGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr NotchModeFr1
%		doublePtr NotchModeFa1
%		doublePtr NotchModeZr1
%		doublePtr NotchModeZa1
%		doublePtr NotchModeFr2
%		doublePtr NotchModeFa2
%		doublePtr NotchModeZr2
%		doublePtr NotchModeZa2


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
NotchModeFr1 = 0;
NotchModeFa1 = 0;
NotchModeZr1 = 0;
NotchModeZa1 = 0;
NotchModeFr2 = 0;
NotchModeFa2 = 0;
NotchModeZr2 = 0;
NotchModeZa2 = 0;

% lib call
[errorCode, PositionerName, NotchModeFr1, NotchModeFa1, NotchModeZr1, NotchModeZa1, NotchModeFr2, NotchModeFa2, NotchModeZr2, NotchModeZa2] = calllib('XPS_C8_drivers', 'PositionerCompensationNotchModeFiltersGet', socketId, PositionerName, NotchModeFr1, NotchModeFa1, NotchModeZr1, NotchModeZa1, NotchModeFr2, NotchModeFa2, NotchModeZr2, NotchModeZa2);
